#!/usr/bin/env python3
"""
Project Cost Calculator

Calculates total project costs including:
- Labor (tracked hours)
- Allocated subscription costs
- Hardware depreciation
- Operational overhead
- Direct API usage costs

Usage:
    python scripts/calculate_project_costs.py --project projects/3m-lighting-garage-organizers.yaml
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json


class ProjectCostCalculator:
    """Calculate comprehensive project costs"""

    def __init__(self, cost_config_path: Path):
        """Initialize with cost configuration"""
        with open(cost_config_path) as f:
            self.config = yaml.safe_load(f)

    def calculate_labor_costs(self, project: Dict) -> Dict[str, float]:
        """Calculate labor costs from tracked time"""
        hours = project['time_tracking']['hours']
        labor_rates = self.config['labor']['task_categories']
        default_rate = self.config['labor']['consultant_hourly_rate']

        costs_by_category = {}
        total = 0.0

        for category, category_hours in hours.items():
            rate = labor_rates.get(category, default_rate)
            cost = category_hours * rate
            costs_by_category[category] = cost
            total += cost

        return {
            'by_category': costs_by_category,
            'total': total,
            'total_hours': sum(hours.values())
        }

    def calculate_subscription_allocation(self, project: Dict) -> Dict[str, float]:
        """
        Allocate subscription costs to project based on duration and intensity

        Formula: (Monthly Cost) * (Project Work Days / Available Work Days)
        """
        project_days = project['project_metrics']['active_work_days']
        total_work_days_per_month = 20  # Standard work month

        allocation_factor = min(project_days / total_work_days_per_month, 1.0)

        subscriptions = self.config['subscriptions']
        allocated_costs = {}
        total = 0.0

        # Flatten subscription categories
        for category, services in subscriptions.items():
            for service, details in services.items():
                # Only allocate if service was used in project
                if service in project.get('tools_used', []):
                    cost = details['cost'] * allocation_factor
                    allocated_costs[f"{category}.{service}"] = cost
                    total += cost

        return {
            'by_service': allocated_costs,
            'total': total,
            'allocation_factor': allocation_factor,
            'notes': f"Allocated {allocation_factor*100:.1f}% of subscription costs"
        }

    def calculate_hardware_allocation(self, project: Dict) -> Dict[str, float]:
        """
        Allocate hardware depreciation based on usage time

        Formula: (Monthly Depreciation) * (Project Hours / Total Work Hours)
        """
        project_hours = sum(project['time_tracking']['hours'].values())
        monthly_work_hours = 160  # Standard work month

        allocation_factor = min(project_hours / monthly_work_hours, 1.0)

        hardware = self.config['hardware']
        allocated_costs = {}
        total = 0.0

        for device, details in hardware.items():
            if details.get('fully_depreciated', False):
                continue

            cost = details['monthly_depreciation'] * allocation_factor
            allocated_costs[device] = cost
            total += cost

        return {
            'by_device': allocated_costs,
            'total': total,
            'allocation_factor': allocation_factor,
            'notes': f"Allocated {allocation_factor*100:.1f}% of hardware costs"
        }

    def calculate_operational_allocation(self, project: Dict) -> Dict[str, float]:
        """
        Allocate operational costs as overhead

        Formula: (Total Monthly Operational / Monthly Work Hours) * Project Hours
        """
        operational = self.config['operational']

        # Flatten nested operational costs
        total_monthly_operational = 0.0
        for category in operational.values():
            if isinstance(category, dict) and 'cost' in category:
                total_monthly_operational += category['cost']
            elif isinstance(category, dict):
                # Nested structure, sum all costs
                for service in category.values():
                    if isinstance(service, dict) and 'cost' in service:
                        total_monthly_operational += service['cost']

        project_hours = sum(project['time_tracking']['hours'].values())
        monthly_work_hours = 160

        hourly_operational_rate = total_monthly_operational / monthly_work_hours if monthly_work_hours > 0 else 0
        total = hourly_operational_rate * project_hours

        return {
            'total_monthly_operational': total_monthly_operational,
            'hourly_rate': hourly_operational_rate,
            'project_hours': project_hours,
            'total': total
        }

    def calculate_api_costs(self, project: Dict) -> Dict[str, Any]:
        """Calculate direct API usage costs"""
        api_usage = project.get('api_usage', {})
        api_pricing = self.config['api_pricing']

        costs_by_service = {}
        total = 0.0

        # OpenAI Whisper
        if 'whisper_minutes' in api_usage:
            minutes = api_usage['whisper_minutes']
            cost_per_min = api_pricing['openai']['whisper']['cost_per_minute']
            cost = minutes * cost_per_min
            costs_by_service['openai_whisper'] = {
                'units': minutes,
                'unit_type': 'minutes',
                'cost': cost
            }
            total += cost

        # OpenAI GPT-4 Vision
        if 'gpt4_vision_images' in api_usage:
            images = api_usage['gpt4_vision_images']
            cost_per_image = api_pricing['openai']['gpt4_vision']['cost_per_image']
            cost = images * cost_per_image
            costs_by_service['openai_gpt4_vision'] = {
                'units': images,
                'unit_type': 'images',
                'cost': cost
            }
            total += cost

        # Anthropic Claude
        if 'claude_input_tokens' in api_usage:
            input_tokens = api_usage['claude_input_tokens']
            output_tokens = api_usage.get('claude_output_tokens', 0)
            input_cost = (input_tokens / 1_000_000) * api_pricing['anthropic']['claude_sonnet']['input_cost_per_1M_tokens']
            output_cost = (output_tokens / 1_000_000) * api_pricing['anthropic']['claude_sonnet']['output_cost_per_1M_tokens']
            cost = input_cost + output_cost
            costs_by_service['anthropic_claude'] = {
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': cost
            }
            total += cost

        # Apify
        if 'apify_results' in api_usage:
            results = api_usage['apify_results']
            # Apify costs are included in subscription for compute units
            costs_by_service['apify'] = {
                'units': results,
                'unit_type': 'results',
                'cost': 0.0,
                'notes': 'Included in subscription'
            }

        # BrightData
        if 'brightdata_requests' in api_usage:
            requests = api_usage['brightdata_requests']
            cost_per_1k = api_pricing['bright_data']['web_unlocker']['cost_per_1k_requests']
            cost = (requests / 1000) * cost_per_1k
            costs_by_service['brightdata'] = {
                'units': requests,
                'unit_type': 'requests',
                'cost': cost
            }
            total += cost

        return {
            'by_service': costs_by_service,
            'total': total
        }

    def calculate_total_costs(self, project: Dict) -> Dict[str, Any]:
        """Calculate all project costs"""
        labor = self.calculate_labor_costs(project)
        subscriptions = self.calculate_subscription_allocation(project)
        hardware = self.calculate_hardware_allocation(project)
        operational = self.calculate_operational_allocation(project)
        api = self.calculate_api_costs(project)

        # Calculate totals
        total_direct_costs = (
            labor['total'] +
            subscriptions['total'] +
            hardware['total'] +
            operational['total'] +
            api['total']
        )

        # Apply markup if specified
        markup_pct = project.get('pricing', {}).get('markup_percentage', 50)
        markup_amount = total_direct_costs * (markup_pct / 100)
        quoted_price = total_direct_costs + markup_amount

        return {
            'project_name': project['project_name'],
            'client': project.get('client', 'N/A'),
            'date_calculated': datetime.now().isoformat(),

            'breakdown': {
                'labor': labor,
                'subscriptions': subscriptions,
                'hardware': hardware,
                'operational': operational,
                'api_costs': api
            },

            'summary': {
                'total_labor': labor['total'],
                'total_subscriptions': subscriptions['total'],
                'total_hardware': hardware['total'],
                'total_operational': operational['total'],
                'total_api': api['total'],
                'total_direct_costs': total_direct_costs,
                'markup_percentage': markup_pct,
                'markup_amount': markup_amount,
                'quoted_price': quoted_price,
                'total_hours': labor['total_hours']
            },

            'metrics': {
                'effective_hourly_rate': quoted_price / labor['total_hours'] if labor['total_hours'] > 0 else 0,
                'cost_per_hour': total_direct_costs / labor['total_hours'] if labor['total_hours'] > 0 else 0,
                'overhead_percentage': ((total_direct_costs - labor['total']) / labor['total'] * 100) if labor['total'] > 0 else 0
            }
        }

    def generate_report(self, project: Dict) -> str:
        """Generate human-readable cost report"""
        costs = self.calculate_total_costs(project)

        report = []
        report.append("=" * 80)
        report.append(f"PROJECT COST ANALYSIS: {costs['project_name']}")
        report.append("=" * 80)
        report.append(f"Client: {costs['client']}")
        report.append(f"Calculated: {costs['date_calculated']}")
        report.append("")

        # Summary
        report.append("COST SUMMARY")
        report.append("-" * 80)
        s = costs['summary']
        report.append(f"  Labor (#{s['total_hours']:.1f} hours):        ${s['total_labor']:>12,.2f}")
        report.append(f"  Subscriptions:              ${s['total_subscriptions']:>12,.2f}")
        report.append(f"  Hardware Depreciation:      ${s['total_hardware']:>12,.2f}")
        report.append(f"  Operational Overhead:       ${s['total_operational']:>12,.2f}")
        report.append(f"  API Usage:                  ${s['total_api']:>12,.2f}")
        report.append(f"                              {'─' * 20}")
        report.append(f"  TOTAL DIRECT COSTS:         ${s['total_direct_costs']:>12,.2f}")
        report.append("")
        report.append(f"  Markup ({s['markup_percentage']}%):              ${s['markup_amount']:>12,.2f}")
        report.append(f"                              {'═' * 20}")
        report.append(f"  QUOTED PRICE:               ${s['quoted_price']:>12,.2f}")
        report.append("")

        # Metrics
        report.append("KEY METRICS")
        report.append("-" * 80)
        m = costs['metrics']
        report.append(f"  Effective Hourly Rate:      ${m['effective_hourly_rate']:>12,.2f}")
        report.append(f"  Cost Per Hour:              ${m['cost_per_hour']:>12,.2f}")
        report.append(f"  Overhead %:                 {m['overhead_percentage']:>12,.1f}%")
        report.append("")

        # Labor breakdown
        report.append("LABOR BREAKDOWN")
        report.append("-" * 80)
        for category, cost in costs['breakdown']['labor']['by_category'].items():
            hours = project['time_tracking']['hours'][category]
            rate = cost / hours if hours > 0 else 0
            report.append(f"  {category:<30} {hours:>6.1f}h @ ${rate:>6.2f}/h = ${cost:>10,.2f}")
        report.append("")

        # API Usage
        if costs['breakdown']['api_costs']['by_service']:
            report.append("API USAGE COSTS")
            report.append("-" * 80)
            for service, details in costs['breakdown']['api_costs']['by_service'].items():
                if 'units' in details:
                    report.append(f"  {service:<30} {details['units']:>10,} {details['unit_type']:<10} ${details['cost']:>10,.2f}")
                else:
                    # For services without unit tracking
                    notes = details.get('notes', '')
                    report.append(f"  {service:<30} ${details['cost']:>10,.2f}  {notes}")
            report.append("")

        report.append("=" * 80)

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Calculate project costs")
    parser.add_argument(
        '--project',
        type=Path,
        required=True,
        help='Path to project cost tracking YAML file'
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/cost_configuration.yaml'),
        help='Path to cost configuration file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output JSON file for cost data'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'both'],
        default='text',
        help='Output format'
    )

    args = parser.parse_args()

    # Load project
    with open(args.project) as f:
        project = yaml.safe_load(f)

    # Calculate costs
    calculator = ProjectCostCalculator(args.config)
    costs = calculator.calculate_total_costs(project)

    # Output
    if args.format in ['text', 'both']:
        print(calculator.generate_report(project))

    if args.format in ['json', 'both']:
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(costs, f, indent=2)
            print(f"\nCost data saved to: {args.output}")
        else:
            print("\n" + json.dumps(costs, indent=2))


if __name__ == '__main__':
    main()
